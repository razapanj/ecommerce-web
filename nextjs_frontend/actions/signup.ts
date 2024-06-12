export const signUp = async (user_data: User): Promise<any> => {
    try {
        console.log(process.env.URL);
        if (user_data.password === user_data.confirm_password) {
            const user = await fetch(`http://localhost:8000/api/signup`, {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(user_data),
            })
            if (user.ok) {
                const user_response: UserResponse = await user.json()
                console.log(user_response);
                return { "message": "You have been Signup successfully" }
            }
        }
    } catch (error) {
        console.error(error)
    }
}

