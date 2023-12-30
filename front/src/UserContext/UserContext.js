import React, { createContext, useState, useContext } from 'react';

export const AuthContext = createContext({
  token: '',
  isLoggedIn: false,
  username: '',
  login: (token, username) => {},
  logout: () => {},
});

export const AuthContextProvider = ({ children }) => {
  const [token, setToken] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [username, setUsername] = useState('');

  const login = (userToken, userUsername) => {
    setToken(userToken);
    setUsername(userUsername);
    setIsLoggedIn(true);
  };

  const logout = () => {
    setToken('');
    setUsername('');
    setIsLoggedIn(false);
  };

  const contextValue = {
    token: token,
    isLoggedIn: isLoggedIn,
    username: username,
    login: login,
    logout: logout,
  };

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  return useContext(AuthContext);
};
