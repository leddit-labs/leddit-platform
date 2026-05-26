import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { handleCallback } from "../utils/auth";

export default function Callback() {
  const navigate = useNavigate();

  useEffect(() => {
    handleCallback()
      .then(() => navigate("/"))
      .catch(() => navigate("/login?error=auth_failed"));
  }, []);

  return <p>Signing you in...</p>;
}