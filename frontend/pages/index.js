import {useRouter} from "next/router";
import {useAuth} from "../common/auth-context";
import {useEffect, useState} from "react";
import {useMovies} from "../common/use-data";
import {onChange} from "../common/utils";
import { Input, Spacer, Grid, Table, Loading } from "@nextui-org/react";

export default function Home() {
    const router = useRouter();
    const {user} = useAuth();
    const [query, setQuery] = useState('');
    const {data, loading} = useMovies(query);

    useEffect(() => {
        if (!user) {
            router.replace("/login")
        }
    }, [user])

    if (!user) return null;

    return (
        <Grid.Container gap={2} direction="column">
            <Grid>
                <Input placeholder="Search movies" onChange={onChange(setQuery)} />
            </Grid>
            <Spacer />
            <Grid>
                <Table>
                    <Table.Header>
                        <Table.Column>ID</Table.Column>
                        <Table.Column>TITLE</Table.Column>
                        <Table.Column>GENRES</Table.Column>
                    </Table.Header>
                    <Table.Body>
                        {data.map(movie => (
                            <Table.Row key={movie.id}>
                                <Table.Cell>{movie.id}</Table.Cell>
                                <Table.Cell>{movie.title}</Table.Cell>
                                <Table.Cell>{movie.genres.join(", ")}</Table.Cell>
                            </Table.Row>
                        ))}
                    </Table.Body>
                </Table>
            </Grid>
        </Grid.Container>
    )
}