import {useEffect, useState} from "react";
import {useAuth} from "./auth-context";

export function useMovies(query = null) {
    const {user} = useAuth();
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (!user) return;
        refetch();
    }, [query, user])

    function refetch() {
        const args = query ? `?q=${query}` : '';
        setLoading(true);
        return fetch(`http://localhost:3001/user/${user.id}/movie` + args)
            .then(res => res.json())
            .then(data => setData(data))
            .catch(error => alert(error.toString()))
            .finally(() => setLoading(false))
    }

    return {data, loading, refetch};
}

export function useRating() {
    const {user} = useAuth();
    const [submitting, setSubmitting] = useState(false);

    function rateMovie(movieId, rating) {
        setSubmitting(true);
        return fetch("http://localhost:3001/rating",  {
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

export function useRecommendations() {
    const {user} = useAuth();
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (!user) return;
        refetch();
    }, [user])

    function refetch() {
        setLoading(true);
        return fetch(`http://localhost:3001/user/${user.id}/recommended`)
            .then(res => res.json())
            .then(data => setData(data))
            .catch(error => alert(error.toString()))
            .finally(() => setLoading(false))
    }

    return {loading, data, refetch}
}