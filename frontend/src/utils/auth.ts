import { endpoints } from "../api/endpoints";

const CLIENT_ID = "leddit-frontend";
const REDIRECT_URI = window.location.origin + "/callback";

function generateCodeVerifier(): string {
  const array = new Uint8Array(64);
  crypto.getRandomValues(array);
  return btoa(String.fromCharCode(...array))
    .replace(/\+/g, "-")
    .replace(/\//g, "_")
    .replace(/=+$/, "");
}

async function generateCodeChallenge(verifier: string): Promise<string> {
  const encoder = new TextEncoder();
  const data = encoder.encode(verifier);
  const hash = await crypto.subtle.digest("SHA-256", data);
  return btoa(String.fromCharCode(...new Uint8Array(hash)))
    .replace(/\+/g, "-")
    .replace(/\//g, "_")
    .replace(/=+$/, "");
}

export async function login(): Promise<void> {
  const verifier = generateCodeVerifier();
  const challenge = await generateCodeChallenge(verifier);
  const state = generateCodeVerifier();

  sessionStorage.setItem("pkce_verifier", verifier);
  sessionStorage.setItem("oauth_state", state);

  const params = new URLSearchParams({
    client_id: CLIENT_ID,
    response_type: "code",
    redirect_uri: REDIRECT_URI,
    scope: "openid profile email",
    state,
    code_challenge: challenge,
    code_challenge_method: "S256",
  });

  window.location.href = `${endpoints.auth.login}?${params}`;
}

export async function handleCallback(): Promise<void> {
  const params = new URLSearchParams(window.location.search);
  const code = params.get("code");
  const state = params.get("state");

  const savedState = sessionStorage.getItem("oauth_state");
  if (state !== savedState) {
    throw new Error("Invalid state");
  }

  const verifier = sessionStorage.getItem("pkce_verifier");

  const response = await fetch(endpoints.auth.token, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      grant_type: "authorization_code",
      client_id: CLIENT_ID,
      code: code!,
      redirect_uri: REDIRECT_URI,
      code_verifier: verifier!,
    }),
  });

  const tokens = await response.json();

  localStorage.setItem("access_token", tokens.access_token);
  localStorage.setItem("refresh_token", tokens.refresh_token);
  if (tokens.id_token) {
    localStorage.setItem("id_token", tokens.id_token);
  }

  sessionStorage.removeItem("pkce_verifier");
  sessionStorage.removeItem("oauth_state");
}

export async function logout(): Promise<void> {
  const idToken = localStorage.getItem("id_token");

  const params = new URLSearchParams({
    post_logout_redirect_uri: window.location.origin,
  });

  if (idToken) {
    params.set("id_token_hint", idToken);
  }

  localStorage.clear();
  sessionStorage.clear();
  window.location.href = `${endpoints.auth.logout}?${params}`;
}

export function isAuthenticated(): boolean {
  return !!localStorage.getItem("access_token");
}

export async function getUserInfo(): Promise<any> {
  const token = localStorage.getItem("access_token");
  const response = await fetch(endpoints.auth.userinfo, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.json();
}