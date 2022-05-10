export function onChange(callback) {
    return (e) => callback(e.target.value);
}