import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Button, Container, Heading } from "@chakra-ui/react";
import Navbar from "./components/Navbar";
import Callback from "./pages/Callback";
import { usePosts } from "./api/domain/posts/usePosts";

function HomePage() {
  const { posts, page, loadPosts } = usePosts(1, 3);
  return (
    <>
      <Navbar />
      <Container centerContent mt={10}>
        <Heading mb={4}>Leddit the platform deluxe woop</Heading>
        <Button color="brand.500">Click here lmao xd</Button>
      </Container>
      <div>
        <br />
        <div>This below will only show posts if you have posts in your post db</div>
        <div>Try Press "Prev" and "Next"</div>
        <br />
        <button onClick={() => loadPosts(page - 1)}>Prev</button>
        <button onClick={() => loadPosts(page + 1)}>Next</button>
        {posts.map((p) => (
          <div key={p.u_id}>{p.title}</div>
        ))}
      </div>
    </>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/callback" element={<Callback />} />
        <Route path="*" element={<HomePage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;