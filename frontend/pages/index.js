import {useRouter} from "next/router";
import {useAuth} from "../common/auth-context";
import {useEffect, useState} from "react";
import {useRating, useRecommendations} from "../common/use-data";
import {Grid, Button, Text, Tooltip, Loader, Loading} from "@nextui-org/react";
import MovieCard from "../components/MovieCard";
import AppLayout from "../components/Layout";
import IconButton from "../components/IconButton";
import {GrRefresh} from "react-icons/gr";

function getMessage(error) {
    switch (error.message) {
        case "User not present in model": {
            return "You must at least 10 movies, before our recommendations are ready."
        }
        default: {
            return error.message
        }
    }
}

export default function Home() {
    const router = useRouter();
    const {user} = useAuth();
    const {data, invalidate, loading, error} = useRecommendations();

    useEffect(() => {
        if (!user) {
            router.replace("/login")
        }
    }, [user])

    if (!user) return null;

    return (
        <AppLayout>
            <Grid.Container gap={2} direction="column">
                <Grid>
                    <Grid.Container gap={2} direction="row">
                        <Grid>
                            <Text h2>Recommended for you</Text>
                        </Grid>
                        <Grid css={{display: 'flex', justifyContent: 'center'}}>
                            <Tooltip content="Refresh recommendations">
                                <IconButton onClick={invalidate}>
                                    <GrRefresh />
                                </IconButton>
                            </Tooltip>
                        </Grid>
                    </Grid.Container>
                </Grid>
                <Grid>
                    <Grid.Container gap={2}>
                        {error && (
                            <Grid>
                                <Text>{getMessage(error)}</Text>
                            </Grid>
                        )}
                        {loading && !error && (
                            <Grid>
                                <Loading color="currentColor" size="sm" />
                            </Grid>
                        )}
                        {data && data.map(movie => (
                            <Grid xs={4} key={movie.id}>
                                <MovieCard
                                    id={movie.id}
                                    title={movie.title}
                                    posterUrl={movie.poster_url}
                                    overview={movie.overview}
                                    predictedRating={movie.predicted_rating}
                                />
                            </Grid>
                        ))}
                    </Grid.Container>
                </Grid>
            </Grid.Container>
        </AppLayout>
    )
}