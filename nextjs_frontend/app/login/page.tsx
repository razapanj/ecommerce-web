"use client"
import Login from "@/actions/login"
import LoginForm from "@/components/loginform"
import { useState } from "react"
import { useRouter } from "next/navigation"
import { toast } from "react-toastify"

const LoginPage = () => {
    const router = useRouter()
    const [loginusername, setLoginUsername] = useState("")
    const [loginpassword, setLoginpassword] = useState("")
    const submitLogin = async () => {
        const formdata = new URLSearchParams()
        console.log(formdata);
        formdata.append("username", loginusername)
        formdata.append("password", loginpassword)
        const message = await Login(formdata)
        router.push("/")
        toast.success(message?.message)
    }
    return (
        <section>
            <div className="">
                <LoginForm username={loginusername} password={loginpassword} formSubmit={submitLogin} setLoginUsername={setLoginUsername} setLoginpassword={setLoginpassword} />
            </div>
        </section>
    )
}
export default LoginPage