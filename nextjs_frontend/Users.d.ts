interface UserRole {
    admin: string = "admin"
    user: string = "user"
}

interface User {
    username: string
    password: string
    role: string
    firstname: string
    lastname: string
    email: string
    confirm_password: string
    created_at?: Date
    logged_in?: boolean
}

interface UserResponse {
    user_id: number
    username: string
    email: string
    created_at: Date
}