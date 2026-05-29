import { Button, HStack } from "@chakra-ui/react";

type Props = {
  page: number;
  onPrev: () => void;
  onNext: () => void;
};

export default function PostPagination({ page, onPrev, onNext }: Props) {
  return (
    <HStack justify="center" mt={6} spacing={4}>
      {page > 1 && (
        <button onClick={onPrev}>
          Prev
        </button>
      )}

      <Button onClick={onNext} size="sm">
        Next ({page})
      </Button>
    </HStack>
  );
}