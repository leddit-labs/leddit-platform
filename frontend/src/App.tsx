import { Button, Container, Heading } from "@chakra-ui/react";
import Navbar from "./components/Navbar";
import { usePosts } from "./api/domain/posts/usePosts";
import { useState } from "react";

function App() {
  const [page, setPage] = useState(1);

  const { data, isLoading, isError } = usePosts(page, 3);

  const posts = data ?? [];

  return (
    <>
      <Navbar />

      <Container centerContent mt={10}>
        <Heading mb={4}>Leddit the platform deluxe woop</Heading>
        <Button color="brand.500">Click here lmao xd</Button>
      </Container>

      <div>
        <button onClick={() => setPage((p) => Math.max(1, p - 1))}>Prev</button>

        <button onClick={() => setPage((p) => p + 1)}>Next</button>

        {isLoading && <div>Loading...</div>}

        {isError && <div>Something broke</div>}

        {posts.map((p) => (
          <div key={p.u_id}>{p.title}</div>
        ))}
      </div>
    </>
  );
}

export default App;
