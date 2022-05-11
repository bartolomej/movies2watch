import React from "react";
import styled from "styled-components";
import { Col, Container, Row, useTheme } from "@nextui-org/react";
import Link from "./link";

function Navigation() {
    const { theme } = useTheme();
    return (
        <NavContainer>
            <Nav style={{ background: theme?.colors?.purple500 }}>
                <Container style={{ maxWidth: '100%', height: '100%' }}>
                    <Row style={{ height: "100%" }}>
                        <LeftCol>
                            <Link href="/" title="Recommended" />
                            <Link href="/movies" title="Movies" />
                        </LeftCol>
                        <RightCol>

                        </RightCol>
                    </Row>
                </Container>
            </Nav>
        </NavContainer>
    );
}

const NavContainer = styled.div`
  padding: var(--nextui-space-sm);
  * {
    z-index: 100;
  }
`;

const Nav = styled.nav`
  border-radius: 10px;
  height: 60px;
`;

const NavCol = styled(Col)`
  display: flex;
  align-items: center;
  height: 100%;
`;

const LeftCol = styled(NavCol)``;

const RightCol = styled(NavCol)`
  justify-content: flex-end;
`;

export default Navigation;