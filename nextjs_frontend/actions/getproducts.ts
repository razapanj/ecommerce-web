export const getProducts = (): any => {
    try {
        const products = fetch("", {
            body: null,
            headers: {

            }
        })
    } catch (error) {
        console.error(error)
    }
}
