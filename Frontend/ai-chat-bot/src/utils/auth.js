import { jwtDecode } from "jwt-decode";

export const getUserFromToken = (token) => {
  try {
    if (!token) return null;
    const decoded = jwtDecode(token);
    return decoded; // contains name, email, id etc.
  } catch (error) {
    console.error("Invalid token");
    return null;
  }
};
