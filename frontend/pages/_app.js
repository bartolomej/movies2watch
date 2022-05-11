import {createGlobalStyle, ThemeProvider} from 'styled-components'
import {AuthProvider} from "../common/auth-context";
import {NextUIProvider} from '@nextui-org/react';
import {SWRConfig} from 'swr'
import fetcher from "../common/fetcher";

const GlobalStyle = createGlobalStyle`
  body {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }
`

const theme = {
    colors: {
        primary: '#0070f3',
    },
}

export default function App({Component, pageProps}) {
    return (
        <>
            <GlobalStyle/>
            <ThemeProvider theme={theme}>
                <AuthProvider>
                    <NextUIProvider>
                        <SWRConfig value={{
                            refreshInterval: 3000,
                            fetcher
                        }}>
                            <Component {...pageProps} />
                        </SWRConfig>
                    </NextUIProvider>
                </AuthProvider>
            </ThemeProvider>
        </>
    )
}