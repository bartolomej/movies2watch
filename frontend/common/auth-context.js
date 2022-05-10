import React, {useContext, useMemo, useState} from "react";

const AuthContext = React.createContext({
    user: null,
    setUser: () => {
    }
});

export function AuthProvider({children}) {
    const [user, setUser] = useState(null);

    const value = useMemo(
        () => ({user, setUser}),
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