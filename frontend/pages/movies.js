import {useRouter} from "next/router";
import {useAuth} from "../common/auth-context";
import {useEffect, useState} from "react";
import {useMovies, useRating, useRecommendations} from "../common/use-data";
import {onChange} from "../common/utils";
import {styled} from "@nextui-org/react";
import {Input, Spacer, Grid, Table, Modal, Row, Col, Tooltip, Button, Text, Avatar} from "@nextui-org/react";
import RateModal from "../components/RateModal";
import {FaStar} from "react-icons/fa"
import {MdRateReview} from "react-icons/md"
import IconButton from "../components/IconButton";
import AppLayout from "../components/Layout";

export default function Home() {
    const router = useRouter();
    const {user} = useAuth();
    const [currMovieId, setCurrMovieId] = useState(null);
    const [query, setQuery] = useState('');
    const {data, loading, refetch} = useMovies(query);
    const {submitting, rateMovie} = useRating()

    useEffect(() => {
        if (!user) {
            router.replace("/login")
        }
    }, [user])

    async function onSubmitRating(rating) {
        await rateMovie(currMovieId, rating);
        await refetch();
        setCurrMovieId(null);
    }

    if (!user) return null;

    return (
        <AppLayout>
            <Grid.Container gap={2} direction="column">
                <RateModal
                    open={currMovieId !== null}
                    onClose={() => setCurrMovieId(null)}
                    onSubmit={onSubmitRating}
                    submitting={submitting}
                />
                <Grid>
                    <Grid.Container gap={2} direction="row">
                        <Grid>
                            <Text h2>Movies</Text>
                        </Grid>
                        <Grid css={{display: 'flex', justifyContent: 'center'}}>
                            <Input placeholder="Search movies" onChange={onChange(setQuery)}/>
                        </Grid>
                    </Grid.Container>
                </Grid>
                <Grid>
                    <Grid.Container gap={2}>
                        <Grid>
                            <Table>
                                <Table.Header>
                                    <Table.Column>ID</Table.Column>
                                    <Table.Column></Table.Column>
                                    <Table.Column>TITLE</Table.Column>
                                    <Table.Column>GENRES</Table.Column>
                                    <Table.Column>RATING</Table.Column>
                                    <Table.Column></Table.Column>
                                </Table.Header>
                                <Table.Body>
                                    {data.map(movie => (
                                        <Table.Row key={movie.id}>
                                            <Table.Cell>{movie.id}</Table.Cell>
                                            <Table.Cell>
                                                <Avatar squared src={movie.poster_url} />
                                            </Table.Cell>
                                            <Table.Cell>{movie.title}</Table.Cell>
                                            <Table.Cell>{movie.genres.join(", ")}</Table.Cell>
                                            <Table.Cell>
                                                {movie.rating && (
                                                    <>{movie.rating} <FaStar /></>
                                                )}
                                            </Table.Cell>
                                            <Table.Cell>
                                                <Row justify="center" align="center">
                                                    <Col css={{d: "flex"}}>
                                                        {!movie.rating && (
                                                            <IconButton onClick={() => setCurrMovieId(movie.id)}>
                                                                <MdRateReview />
                                                            </IconButton>
                                                        )}
                                                    </Col>
                                                </Row>
                                            </Table.Cell>
                                        </Table.Row>
                                    ))}
                                </Table.Body>
                            </Table>
                        </Grid>
                    </Grid.Container>
                </Grid>
            </Grid.Container>
        </AppLayout>
    )
}