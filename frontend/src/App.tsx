import { Button, Container, Heading } from "@chakra-ui/react";
import Navbar from "./components/Navbar";
import { usePosts } from "./api/hooks/usePosts";

function App() {
	const { posts, page, loadPosts } = usePosts();
	console.log(posts)
  return (
    <>
      <Navbar />

      <Container centerContent mt={10}>
        <Heading mb={4}>Leddit the platform deluxe woop</Heading>
        <Button color="brand.500">Click here lmao xd</Button>
      </Container>

      <div>
        <button onClick={() => loadPosts(page - 1)}>Prev</button>
        <button onClick={() => loadPosts(page + 1)}>Next</button>

        {posts.map((p) => (
          <div key={p.id}>{p.title}</div>
        ))}
      </div>
    </>
  );
}

export default App;
