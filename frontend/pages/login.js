import {useState} from "react";
import {onChange} from "../common/utils";
import {Grid, Card, Text, Input, Spacer, Button, Loading} from "@nextui-org/react";
import useLogin from "../common/use-login";

export default function Login() {
    const {loading, submit} = useLogin();
    const [username, setUsername] = useState();
    const [password, setPassword] = useState();

    function onSubmit(e) {
        e.preventDefault();
        submit(username, password)
    }

    return (
        <Grid.Container gap={2} justify="center" css={{height: '100vh', alignItems: 'center'}}>
            <Grid xs={4}>
                <Card>
                    <Grid>
                        <Text h3 css={{textAlign: 'center'}} color="gradient">
                            Login
                        </Text>
                    </Grid>
                    <Spacer y={1.6}/>
                    <Grid>
                        <Input
                            labelPlaceholder="Username"
                            css={{width: '100%'}}
                            type="text"
                            placeholder="Username"
                            onChange={onChange(setUsername)}
                        />
                    </Grid>
                    <Spacer/>
                    <Grid>
                        <Input
                            labelPlaceholder="Password"
                            css={{width: '100%'}}
                            type="password"
                            placeholder="Password"
                            onChange={onChange(setPassword)}
                        />
                    </Grid>
                    <Spacer/>
                    <Grid>
                        <Button
                            disabled={loading}
                            bordered
                            color="gradient"
                            style={{width: '100%'}}
                            onClick={onSubmit}
                        >
                            {loading ? <Loading color="currentColor" size="sm" /> : 'Login'}
                        </Button>
                    </Grid>
                </Card>
            </Grid>
        </Grid.Container>
    )
}
