import {useState} from "react";
import {useAuth} from "./auth-context";
import {useRouter} from "next/router";

export default function useRegistration() {
    const router = useRouter();
    const [loading, setLoading] = useState(false);

    function submit(username, password) {
        setLoading(true)
        return fetch("http://localhost:3001/user", {
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
                return router.replace("/login")
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