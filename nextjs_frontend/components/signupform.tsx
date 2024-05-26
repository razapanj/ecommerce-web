import { FormEvent } from "react"

interface UserProps {
    username: string
    email: string
    firstname: string
    lastname: string
    password: string
    confirm_password: string
    role: UserRole
    setUsername: (username: string) => void;
    setEmail: (email: string) => void;
    setFirstName: (firstName: string) => void;
    setLastName: (lastName: string) => void;
    setPassword: (password: string) => void;
    setConfirmPassword: (confirmPassword: string) => void;
    setRole: (role: UserRole) => void;
    onsubmit: (event: FormEvent<HTMLFormElement>) => any;
}

const Signupform = (props: UserProps) => {

    let { username, email, firstname, lastname, password, confirm_password, role, setUsername, setEmail, setFirstName, setLastName, setPassword, setConfirmPassword, setRole, onsubmit } = props

    return (
        <>
            <form action="" onSubmit={(event) => { onsubmit(event) }}>
                <input type="text" name="username" id="" value={username} onChange={(e) => { setUsername(e.target.value) }} />
                <input type="email" name="email" id="" value={email} onChange={(e) => { setEmail(e.target.value) }} />
                <input type="text" name="firstName" id="" value={firstname} onChange={(e) => { setFirstName(e.target.value) }} />
                <input type="text" name="lastName" id="" value={lastname} onChange={(e) => { setLastName(e.target.value) }} />
                <input type="password" name="password" id="" value={password} onChange={(e) => { setPassword(e.target.value) }} />
                <input type="password" name="confirmpassword" id="" value={confirm_password} onChange={(e) => { setConfirmPassword(e.target.value) }} />
                <input type="checkbox" name="role" id="" value={role.user} />
                <button type="submit">submit</button>

            </form>
        </>
    )
}
export default Signupform