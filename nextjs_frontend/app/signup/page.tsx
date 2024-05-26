"use client"
import { useState, FormEvent } from "react"
import Signupform from "@/components/signupform"
import { signUp } from "@/actions/signup"
const Signup = () => {
    const [username, setUsername] = useState("")
    const [email, setEmail] = useState("")
    const [firstname, setFirstName] = useState("")
    const [lastname, setLastName] = useState("")
    const [password, setPassword] = useState("")
    const [confirm_password, setConfirmPassword] = useState("")
    const [role, setRole] = useState({ admin: "admin", user: "user" })

    const userInfo = {
        "username": username,
        "email": email,
        "firstname": firstname,
        "lastname": lastname,
        "password": password,
        "confirm_password": confirm_password,
        "role": role?.user
    }

    const handleSignUp = async (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault()
        signUp(userInfo)
    }

    return (
        <>
            <Signupform username={username} email={email} firstname={firstname} lastname={lastname} password={password} confirm_password={confirm_password} role={role} setUsername={setUsername} setEmail={setEmail} setFirstName={setFirstName} setLastName={setLastName} setPassword={setPassword} setConfirmPassword={setConfirmPassword} setRole={setRole} onsubmit={handleSignUp} />
        </>
    )
}
export default Signup