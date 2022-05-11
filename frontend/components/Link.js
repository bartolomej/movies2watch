import React, { ReactChildren, ReactElement } from "react";
import NextLink from "next/link";
import { Link as NextUiLink, Text } from "@nextui-org/react";

function Link({ href, title, style, children }) {
    return (
        <NextLink href={href}>
            <NextUiLink style={style} block color="secondary">
                {title ? (
                    <Text
                        size="$sm"
                        color="gradient"
                        b
                    >
                        {title}
                    </Text>
                ) : (
                    children
                )}
            </NextUiLink>
        </NextLink>
    );
}

export default Link;