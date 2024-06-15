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
        const actionSignUp = await signUp(userInfo)
        console.log(actionSignUp);

    }

    return (
        <section className="m-12 md:m-10 rounded-2xl flex md:flex-row flex-col flex-1 md:items-center md:justify-center items-center justify-center h-screen bg-gradient-to-b from-blue-800 to-indigo-900 text-white">
            <div className="flex flex-col gap-6 md:justify-center md:items-center md:w-full ">
                <h1 className="uppercase text-center text-5xl font-bold">Sign up</h1>
                <Signupform username={username} email={email} firstname={firstname} lastname={lastname} password={password} confirm_password={confirm_password} role={role} setUsername={setUsername} setEmail={setEmail} setFirstName={setFirstName} setLastName={setLastName} setPassword={setPassword} setConfirmPassword={setConfirmPassword} setRole={setRole} onsubmit={handleSignUp} />
            </div>
            <div className="md:flex flex-col items-center justify-center mx-auto h-screen bg-gray-500 hidden">

            </div>
        </section>
    )
}
export default Signup