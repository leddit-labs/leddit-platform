import { Button, Container, Heading } from "@chakra-ui/react";
import Navbar from "./components/Navbar";
import { usePosts } from "./api/domain/posts/usePosts";

function App() {
	const { posts, page, loadPosts } = usePosts(1,3);
  return (
    <>
      <Navbar />

      <Container centerContent mt={10}>
        <Heading mb={4}>Leddit the platform deluxe woop</Heading>
        <Button color="brand.500">Click here lmao xd</Button>
      </Container>

	{/* just some debug test fetching below - will be deleted */}
      <div>
		<br></br>
		<div>This below will only show posts if you have posts in your post db</div>
		<div>Try Press "Prev" and "Next"</div>
		<br></br>
        <button onClick={() => loadPosts(page - 1)}>Prev</button>
        <button onClick={() => loadPosts(page + 1)}>Next</button>
		
        {posts.map((p) => (
          <div key={p.u_id}>{p.title}</div>
        ))}
      </div>
    </>
  );
}

export default App;
