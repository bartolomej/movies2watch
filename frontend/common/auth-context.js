import React, {useContext, useMemo, useState} from "react";

const AuthContext = React.createContext({
    user: null,
    setUser: () => {},
    logout: () => {}
});

export function AuthProvider({children}) {
    const [user, setUser] = useState(null);

    function logout() {
        setUser(null);
    }

    const value = useMemo(
        () => ({user, setUser, logout}),
        [user]
    );

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    )
}

export function useAuth() {
    return useContext(AuthContext);
}