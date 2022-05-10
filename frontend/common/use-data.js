import {useEffect, useState} from "react";

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