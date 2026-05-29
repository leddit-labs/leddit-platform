import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Alert, AlertIcon, Container } from "@chakra-ui/react";
import Navbar from "./components/Navbar";
import Callback from "./pages/Callback";
import { usePosts } from "./api/domain/posts/usePosts";
import { useState } from "react";
import PostGrid from "./components/posts/PostGrid";
import PostPagination from "./components/posts/PostPagination";

function HomePage() {

  const [page, setPage] = useState(1);

  const { data, isLoading, isError } = usePosts(page, 5);

  const posts = data ?? [];

  return (
    <>
      <Navbar />

      <Container maxW="900px" mt={10}>
        {isError && <div>Something broke</div>}

        <PostGrid posts={posts} isLoading={isLoading} />

        {!isLoading && posts.length === 0 && (
          <Alert status="warning">
            <AlertIcon />
            No more posts returned from API. Add some posts to your postDB my friend
          </Alert>
        )}

        <PostPagination
          page={page}
          onPrev={() => setPage((p) => Math.max(1, p - 1))}
          onNext={() => setPage((p) => p + 1)}
        />
      </Container>
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