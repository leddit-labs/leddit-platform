import { Button, Container, Heading } from "@chakra-ui/react"
import Navbar from "./components/Navbar"

function App() {
	return (
		<>
			<Navbar />

			<Container centerContent mt={10}>
				<Heading mb={4}>Leddit the platform deluxe woop</Heading>
				<Button color="brand.500">Click here lmao xd</Button>
			</Container>
		</>
	)
}

export default App