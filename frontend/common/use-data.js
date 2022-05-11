import {useEffect, useState} from "react";
import {useAuth} from "./auth-context";
import useSWR, {useSWRConfig} from 'swr'
import fetcher from "./fetcher";

export function useMovies(query = null) {
    const {user} = useAuth();
    const {mutate} = useSWRConfig()
    const args = query ? `?q=${query}` : '';
    const key = `/user/${user?.id}/movie${args}`;
    const {data, error} = useSWR(key);

    return {data: data, loading: !data, error, invalidate: () => mutate(key)};
}

export function useRating() {
    const {user} = useAuth();
    const {mutate} = useSWRConfig()
    const key = `/user/${user?.id}/movie`;
    const [submitting, setSubmitting] = useState(false);

    function rateMovie(movieId, rating) {
        setSubmitting(true);
        return fetcher("/rating", {
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
            .then(data => mutate(key))
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
    const {mutate} = useSWRConfig();
    const key = `/user/${user?.id}/recommended`;
    const {data, error} = useSWR(key, null, {
        refreshInterval: 0
    });

    return {loading: !data, error, data: data, invalidate: () => mutate(key)}
}