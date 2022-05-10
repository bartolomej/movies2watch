import {useRouter} from "next/router";
import {useAuth} from "../common/auth-context";
import {useEffect, useState} from "react";
import {useMovies} from "../common/use-data";
import {onChange} from "../common/utils";

export default function Home() {
    const router = useRouter();
    const {user} = useAuth();
    const [query, setQuery] = useState('');
    const [movies, loading] = useMovies(query);

    useEffect(() => {
        if (!user) {
            return router.replace("/login")
        }
    }, [user])

    if (!user) return null;

    return (
        <div>
            Hello user {user?.id}
            <input placeholder="Search movies" onChange={onChange(setQuery)} />
            <table>
                <tbody>
                {movies.map(movie => (
                    <tr key={movie.id}>
                        <td>{movie.id}</td>
                        <td>{movie.title}</td>
                        <td>{movie.genres.join(", ")}</td>
                    </tr>
                ))}
                </tbody>
            </table>
        </div>
    )
}