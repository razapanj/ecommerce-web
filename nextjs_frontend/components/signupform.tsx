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
            <form action="" onSubmit={(event) => { onsubmit(event) }} className="flex flex-col gap-2 ">
                <label htmlFor="username">USERNAME</label>
                <input className="outline-none rounded-md text-black p-1" type="text" name="username" id="username" value={username} onChange={(e) => { setUsername(e.target.value) }} />
                <label htmlFor="email">EMAIL</label>
                <input className="outline-none rounded-md text-black p-1" type="email" name="email" id="email" value={email} onChange={(e) => { setEmail(e.target.value) }} />
                <label htmlFor="firstname">FIRSTNAME</label>
                <input className="outline-none rounded-md text-black p-1" type="text" id="firstname" name="firstName" value={firstname} onChange={(e) => { setFirstName(e.target.value) }} />
                <label htmlFor="lastname">LASTNAME</label>
                <input className="outline-none rounded-md text-black p-1" type="text" name="lastName" id="lastname" value={lastname} onChange={(e) => { setLastName(e.target.value) }} />
                <label htmlFor="password">PASSWORD</label>
                <input className="outline-none rounded-md text-black p-1" type="password" id="password" name="password" value={password} onChange={(e) => { setPassword(e.target.value) }} />
                <label htmlFor="confirmpassword">CONFIRMPASSWORD</label>
                <input className="outline-none rounded-md text-black p-1" type="password" name="confirmpassword" value={confirm_password} onChange={(e) => { setConfirmPassword(e.target.value) }} />
                <div className="flex justify-center gap-3">
                    <label htmlFor="admin">ADMIN</label>
                    <input className="outline-none rounded-md text-black p-1" type="checkbox" id="admin" name="role" value={role.user} />
                    <label htmlFor="user">USER</label>
                    <input className="outline-none rounded-md text-black p-1" type="checkbox" name="role" id="user" value={role.user} />
                </div>
                <button type="submit" className="uppercase text-xl mt-2 bg-[#87CEEB] flex justify-center p-1.5 rounded-lg">submit</button>
            </form>
        </>
    )
}
export default Signupform