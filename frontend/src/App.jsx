import {
  Box,
  Flex,
  Input,
  Stack,
  Table,
  Tbody,
  Td,
  Th,
  Thead,
  Tr,
} from "@chakra-ui/react";
import axios from "axios";
import { useEffect, useRef, useState } from "react";
import { useObject } from "./hooks/state";

const baseURL = import.meta.env.VITE_BASE_URL || "/";

function MyImage({ src, bboxes }) {
  const canvasRef = useRef(null);
  const state = useObject({ size: [0, 0] });

  useEffect(() => {
    if (src) {
      const canvas = canvasRef.current;
      const ctx = canvas.getContext("2d");

      const image = new Image();
      image.src = src;

      image.onload = () => {
        console.log("Loaded");
        canvas.width = image.naturalWidth;
        canvas.height = image.naturalHeight;
        state.size = [image.naturalWidth, image.naturalHeight];
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        const hRatio = canvas.width / image.width;
        const vRatio = canvas.height / image.height;
        const ratio = Math.min(hRatio, vRatio);

        ctx.drawImage(
          image,
          0,
          0,
          image.width,
          image.height,
          0,
          0,
          image.width * ratio,
          image.height * ratio
        );
        if (bboxes != null) {
          ctx.filter = "backdrop-blur(10px)";
          ctx.globalCompositeOperation = "destination-top";
          ctx.fillStyle = "#00FFFF";
          ctx.font = "18px Arial";
          ctx.strokeStyle = "#14D514";
          ctx.lineWidth = 3;
          bboxes.forEach((el) => {
            const [x, y, w, h] = el.bbox;
            var score = el.score;
            score = score.toFixed(2);
            ctx.rect(x, y, w, h);
            ctx.fillText(el.label+' - '+score, x+5, y+15);
            ctx.stroke();
          });
        }
      };
    }
  }, [src, bboxes]);
  console.log("Size", state.size);
  return (
    <Box w={state.size && state.size[0]} h={state.size && state.size[1]}>
      <canvas ref={canvasRef} width={800} height={800} />
    </Box>
  );
}

function App() {
  const state = useObject({ file: null, results: [] });
  const [image, setImage] = useState(null);
  useEffect(() => {
    if (state.file != null) {
      const form = new FormData();
      form.append("file", state.file);
      form.append("args", new Blob(["{}"]));
      setImage(URL.createObjectURL(state.file));
      // let reader = new FileReader();
      // reader.onload = (e) => {
      //   state.image = e.target.result;
      // };
      // reader.readAsDataURL(state.file);
      axios
        .post(baseURL, form, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((resp) => (state.results = resp.data));
    }
  }, [state.file]);
  return (
    <Flex w="100vw" h="100vh" p="2rem" direction={"column"}>
      <Input type="file" onChange={(e) => (state.file = e.target.files[0])} />
      <MyImage src={image} bboxes={state.results} />

      <Table h="20%">
        <Thead>
          <Tr>
            <Th>BBox</Th>
          </Tr>
        </Thead>
        <Tbody>
          {state.results.map((el, i) => (
            <Tr key={i}>
              <Td>{JSON.stringify(el)}</Td>
            </Tr>
          ))}
        </Tbody>
      </Table>
    </Flex>
  );
}

export default App;
