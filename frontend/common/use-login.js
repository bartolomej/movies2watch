import {useState} from "react";
import {useAuth} from "./auth-context";
import {useRouter} from "next/router";

export default function useLogin() {
    const router = useRouter();
    const {setUser} = useAuth();
    const [loading, setLoading] = useState(false);

    function submit(username, password) {
        setLoading(true)
        return fetch("http://localhost:3001/user/login", {
            method: "POST",
            headers: {
                'Content-Type': "application/json"
            },
            body: JSON.stringify({
                username,
                password
            })
        })
            .then(res => res.json())
            .then((data) => {
                if (data?.code && data.code !== 200) {
                    return alert(data.message)
                }
                setUser(data);
                return router.replace("/")
            })
            .catch(e => {
                alert(e.toString())
            })
            .finally(() => {
                setLoading(false);
            })
    }

    return {submit, loading}
}