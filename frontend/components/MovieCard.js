import {Card, Col, Row, Button, Text, Tooltip} from "@nextui-org/react";
import {FaStar} from "react-icons/fa"

const dateRegex = /\([0-9]+\)/;
const MovieCard = ({title, posterUrl, overview, predictedRating}) => {

    return (
        <Card cover css={{w: "100%"}}>
            <Card.Header css={{position: "absolute", zIndex: 1, top: 5, display: 'flex', alignItems: 'start'}}>
                <Col>
                    <Text size={12} weight="bold" transform="uppercase" color="#ffffffAA">
                        {title.match(dateRegex)[0] || ''}
                    </Text>
                    <Text h3 color="white" css={{textShadow: "0 0 4px black"}}>
                        {title.replace(dateRegex, "")}
                    </Text>
                </Col>
                <Col css={{display: 'flex', justifyContent: 'flex-end'}}>
                    <Tooltip content={`Predicted rating ${Math.round(predictedRating * 10) / 10}`}>
                        <Text size={20} weight="bold" transform="uppercase" color="#ffffffAA">
                            {Math.round(predictedRating)} <FaStar/>
                        </Text>
                    </Tooltip>
                </Col>
            </Card.Header>
            <Card.Body>
                <Card.Image
                    src={posterUrl}
                    height={400}
                    width="100%"
                    alt="Movie poster"
                />
            </Card.Body>
            <Card.Footer
                blur
                css={{
                    position: "absolute",
                    bgBlur: "#ffffff",
                    borderTop: "$borderWeights$light solid rgba(255, 255, 255, 0.2)",
                    bottom: 0,
                    zIndex: 1,
                }}
            >
                <Row>
                    <Col>
                        <Text color="#000" size={12}>
                            {overview?.substring(0, 80)}...
                        </Text>
                    </Col>
                    <Col>
                        <Row justify="flex-end">
                            <Button flat auto rounded color="secondary">
                                <Text
                                    css={{color: "inherit"}}
                                    size={12}
                                    weight="bold"
                                    transform="uppercase"
                                >
                                    READ MORE
                                </Text>
                            </Button>
                        </Row>
                    </Col>
                </Row>
            </Card.Footer>
        </Card>
    )
}

export default MovieCard;