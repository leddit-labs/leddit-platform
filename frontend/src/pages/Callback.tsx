import { useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { handleCallback } from "../utils/auth";

function parseJwt(token: string) {
  try {
    const payload = token.split(".")[1];
    const decoded = atob(payload.replace(/-/g, "+").replace(/_/g, "/"));
    return JSON.parse(decoded);
  } catch {
    return {};
  }
}

export default function Callback() {
  const navigate = useNavigate();
  const ran = useRef(false);

  useEffect(() => {
    if (ran.current) return;
    ran.current = true;

    handleCallback()
      .then(() => {
        const token = localStorage.getItem("access_token");
        if (token) {
          const user = parseJwt(token);
          localStorage.setItem("username", user.preferred_username || "User");
        }
        navigate("/");
      })
      .catch(() => navigate("/login?error=auth_failed"));
  }, []);

  return <p>Signing you in...</p>;
}