import { createGlobalStyle, ThemeProvider } from 'styled-components'
import {AuthProvider} from "../common/auth-context";

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

export default function App({ Component, pageProps }) {
  return (
      <>
        <GlobalStyle />
        <ThemeProvider theme={theme}>
          <AuthProvider>
              <Component {...pageProps} />
          </AuthProvider>
        </ThemeProvider>
      </>
  )
}