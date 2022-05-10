import {useState} from "react";
import {useRouter} from "next/router";
import {useAuth} from "../common/auth-context";
import {onChange} from "../common/utils";

export default function Login() {
    const router = useRouter();
    const {setUser} = useAuth();
    const [username, setUsername] = useState();
    const [password, setPassword] = useState();

    function onSubmit(e) {
        e.preventDefault();
        fetch("http://localhost:3001/user/login", {
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
            .then((user) => {
                setUser(user);
                return router.replace("/")
            })
            .catch(e => {
                alert(e.toString())
            })
    }

    return (
        <form onSubmit={onSubmit}>
            <input type="text" placeholder="Username" onChange={onChange(setUsername)}/>
            <input type="password" placeholder="Password" onChange={onChange(setPassword)}/>
            <input type="submit"/>
        </form>
    )
}
