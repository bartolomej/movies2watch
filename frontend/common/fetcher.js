export default function fetcher(url, opts) {
    return fetch(`http://localhost:3001${url}`, opts)
        .then(res => res.json())
        .then(data => data?.code ? Promise.reject(data) : Promise.resolve(data))
}