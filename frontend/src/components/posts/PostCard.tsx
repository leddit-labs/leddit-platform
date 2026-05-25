import { Box, Text, VStack, IconButton,} from "@chakra-ui/react";
import type { Post } from "../../api/domain/posts/post";
import { formatDate } from "../../util/date";
import { ChevronUpIcon, ChevronDownIcon } from "@chakra-ui/icons";
import { useCommunity } from "../../api/domain/community/useCommunity";

type Props = {
  post: Post;
};

export default function PostCard({ post }: Props) {
const { data: community } = useCommunity(post.community_id);

  function handleUpvote() {
    // TODO
  }

  function handleDownvote() {
    // TODO
  }

  return (
    <Box
      display="flex"
      bg="gray.800"
      border="1px solid"
      borderColor="gray.600"
      borderRadius="md"
      p={3}
      _hover={{ bg: "gray.750" }}
    >
      {/* LEFT VOTE COLUMN */}
      <VStack spacing={0} minW="40px" align="center" mr={3}>
        <IconButton
          aria-label="upvote"
          icon={<ChevronUpIcon />}
          size="sm"
          variant="ghost"
          onClick={handleUpvote}
        />

        <Text fontWeight="bold">69</Text>

        <IconButton
          aria-label="downvote"
          icon={<ChevronDownIcon />}
          size="sm"
          variant="ghost"
          onClick={handleDownvote}
        />
      </VStack>

      {/* RIGHT CONTENT */}
      <VStack align="start" spacing={1} flex="1">
        <Text fontWeight="bold" fontSize="md">
          {post.title}
        </Text>

        <Text fontSize="sm" color="gray.300">
          {post.content}
        </Text>

        <Text fontSize="xs" color="gray.500">
          {formatDate(post.created_at)}
        </Text>
      </VStack>
    </Box>
  );
}