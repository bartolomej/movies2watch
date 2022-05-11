import React, { ReactElement } from "react";
import Navigation from "../components/navigation";
import styled from "styled-components";

function AppLayout({ children }) {
    return (
        <div>
            <Navigation />
            <Body>
                <Main>{children}</Main>
            </Body>
        </div>
    );
}

const Body = styled.div`
  display: flex;
  flex-direction: row;
  padding: 20px;
`;
const Main = styled.main`
  flex: 1;
`;

export default AppLayout;