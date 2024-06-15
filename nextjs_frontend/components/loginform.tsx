interface LoginProps {
    username: string,
    password: any,
    formSubmit: () => void
    setLoginUsername: (username: string) => void
    setLoginpassword: (password: any) => void
}
const LoginForm = ({ username, password, formSubmit, setLoginUsername, setLoginpassword }: LoginProps) => {

    return (
        <>
            <form onSubmit={(e) => {
                e.preventDefault()
                formSubmit()
            }}>
                <label htmlFor="username">
                    username
                </label>
                <input type="text" name="username" id="username" value={username} onChange={(e) => {
                    setLoginUsername(e.target.value)
                }} />
                <label htmlFor="password">
                    password
                </label>
                <input type="password" name="password" id="password" value={password} onChange={(e) => {
                    setLoginpassword(e.target.value)
                }} />
                <button type="submit">submit</button>
            </form>
        </>
    )
}
export default LoginForm