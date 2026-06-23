import { Box, Skeleton, VStack } from "@chakra-ui/react";

export default function PostSkeleton() {
  return (
    <Box
      bg="gray.800"
      border="1px solid"
      borderColor="gray.600"
      p={4}
      borderRadius="md"
    >
      <VStack align="start" spacing={3}>
        <Skeleton height="20px" width="60%" />
        <Skeleton height="14px" width="90%" />
        <Skeleton height="14px" width="80%" />
      </VStack>
    </Box>
  );
}