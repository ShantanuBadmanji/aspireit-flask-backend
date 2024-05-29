import { createContext, useContext, useState } from "react";

// Create the AuthContext
const AuthContext = createContext();

// Create the AuthContextProvider component
// eslint-disable-next-line react/prop-types
const AuthContextProvider = ({ children }) => {
  // save the token in localstorage
  const [token, setToken] = useState(localStorage.getItem("token") || "");

  //   function to set the token in localstorage
  const setAuthToken = (newToken) => {
    setToken(newToken);
    localStorage.setItem("token", newToken);
  };
  const resetAuthToken = () => {
    setToken("");
    localStorage.removeItem("token");
  };

  return (
    <AuthContext.Provider value={{ token, setAuthToken, resetAuthToken }}>
      {children}
    </AuthContext.Provider>
  );
};

// Create the useAuth custom hook
const useAuth = () => {
  const auth = useContext(AuthContext);

  if (!auth) {
    throw new Error("useAuth must be used within an AuthContextProvider");
  }

  return auth;
};

// eslint-disable-next-line react-refresh/only-export-components
export { AuthContextProvider, useAuth };
