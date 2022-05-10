import {useRouter} from "next/router";
import {useAuth} from "../common/auth-context";
import {useEffect, useState} from "react";
import {useMovies, useRating} from "../common/use-data";
import {onChange} from "../common/utils";
import {styled} from "@nextui-org/react";
import {Input, Spacer, Grid, Table, Modal, Row, Col, Tooltip, Button, Text} from "@nextui-org/react";
import RateModal from "../components/RateModal";

export default function Home() {
    const router = useRouter();
    const {user} = useAuth();
    const [currMovieId, setCurrMovieId] = useState(null);
    const [query, setQuery] = useState('');
    const {data, loading} = useMovies(query);
    const {submitting, rateMovie} = useRating()

    useEffect(() => {
        if (!user) {
            router.replace("/login")
        }
    }, [user])

    function onSubmitRating(rating) {
        rateMovie(currMovieId, rating);
        setCurrMovieId(null);
    }

    if (!user) return null;

    return (
        <Grid.Container gap={2} direction="column">
            <RateModal
                open={currMovieId !== null}
                onClose={() => setCurrMovieId(null)}
                onSubmit={onSubmitRating}
                submitting={submitting}
            />
            <Grid>
                <Input placeholder="Search movies" onChange={onChange(setQuery)}/>
            </Grid>
            <Spacer/>
            <Grid>
                <Table>
                    <Table.Header>
                        <Table.Column>ID</Table.Column>
                        <Table.Column>TITLE</Table.Column>
                        <Table.Column>GENRES</Table.Column>
                        <Table.Column></Table.Column>
                    </Table.Header>
                    <Table.Body>
                        {data.map(movie => (
                            <Table.Row key={movie.id}>
                                <Table.Cell>{movie.id}</Table.Cell>
                                <Table.Cell>{movie.title}</Table.Cell>
                                <Table.Cell>{movie.genres.join(", ")}</Table.Cell>
                                <Table.Cell>
                                    <Row justify="center" align="center">
                                        <Col css={{d: "flex"}}>
                                            <IconButton onClick={() => setCurrMovieId(movie.id)}>
                                                Rate
                                            </IconButton>
                                        </Col>
                                    </Row>
                                </Table.Cell>
                            </Table.Row>
                        ))}
                    </Table.Body>
                </Table>
            </Grid>
        </Grid.Container>
    )
}

export const IconButton = styled('button', {
    dflex: 'center',
    border: 'none',
    outline: 'none',
    cursor: 'pointer',
    padding: '0',
    margin: '0',
    bg: 'transparent',
    transition: '$default',
    '&:hover': {
        opacity: '0.8'
    },
    '&:active': {
        opacity: '0.6'
    }
});