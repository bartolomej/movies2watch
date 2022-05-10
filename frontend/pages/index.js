import {useRouter} from "next/router";
import {useAuth} from "../common/auth-context";
import {useEffect} from "react";

export default function Home() {
    const router = useRouter();
    const {user} = useAuth();

    useEffect(() => {
        if (!user) {
            router.replace("/login")
        }
    }, [user])

    const [id] = user;
    return (
        <div>
            Hello user {id}
        </div>
    )
}