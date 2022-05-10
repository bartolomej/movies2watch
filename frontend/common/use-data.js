import {useEffect, useState} from "react";
import {useAuth} from "./auth-context";

export function useMovies(query = null) {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        const args = query ? `?q=${query}` : '';
        setLoading(true);
        fetch("http://localhost:3001/movie" + args)
            .then(res => res.json())
            .then(data => setData(data))
            .catch(error => alert(error.toString()))
            .finally(() => setLoading(false))
    }, [query])

    return {data, loading};
}

export function useRating() {
    const {user} = useAuth();
    const [submitting, setSubmitting] = useState(false);

    function rateMovie(movieId, rating) {
        setSubmitting(true);
        fetch("http://localhost:3001/rating",  {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                movie_id: movieId,
                user_id: user.id,
                rating
            })
        })
            .then(res => res.json())
            .then(data => console.log(data))
            .catch(error => alert(error.toString()))
            .finally(() => setSubmitting(false))
    }

    return {
        rateMovie,
        submitting
    }
}