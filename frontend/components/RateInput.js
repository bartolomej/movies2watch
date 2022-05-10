import Rating from "react-rating";
import styled from "styled-components";
import {useTheme} from "@nextui-org/react";

export default function RateInput({ size = 40, ...props }) {
    const { theme } = useTheme();

    const SVGIcon = (props) =>
        <svg className={props.className} width={size} height={size} pointerEvents="none">
            <use xlinkHref={props.href}/>
            <defs>
                <symbol id="icon-star-empty" viewBox="0 0 1024 1024">
                    <title>star-empty</title>
                    <path className="path1" d="M1024 397.050l-353.78-51.408-158.22-320.582-158.216 320.582-353.784 51.408 256 249.538-60.432 352.352 316.432-166.358 316.432 166.358-60.434-352.352 256.002-249.538zM512 753.498l-223.462 117.48 42.676-248.83-180.786-176.222 249.84-36.304 111.732-226.396 111.736 226.396 249.836 36.304-180.788 176.222 42.678 248.83-223.462-117.48z"/>
                </symbol>
                <symbol id="icon-star-full" viewBox="0 0 1024 1024">
                    <title>star-full</title>
                    <path className="path1" d="M1024 397.050l-353.78-51.408-158.22-320.582-158.216 320.582-353.784 51.408 256 249.538-60.432 352.352 316.432-166.358 316.432 166.358-60.434-352.352 256.002-249.538z"/>
                </symbol>
            </defs>
        </svg>;

    return (
        <Container color={theme.colors.primary.value}>
            <Rating
                emptySymbol={<SVGIcon href="#icon-star-empty" className="icon"/>}
                fullSymbol={<SVGIcon href="#icon-star-full" className="icon"/>}
                {...props}
            />
        </Container>
    )
}

const Container = styled.div`
    path {
        fill: ${props => props?.color};
    }
`;