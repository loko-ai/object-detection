import { useState } from "react";

export function useObject(o = null) {
  const [obj, setObj] = useState(o != null ? o : {});
  const p = new Proxy(obj, {
    set: (obj, key, value) => {
      setObj({ ...obj, [key]: value });
      console.log("Key", key);
      return true;
    },
  });
  return p;
}

export function useArray(arr = null) {
  const [value, setValue] = useState(arr ? [...arr] : []);
  const additional = {
    push: (el) => setValue([...value, el]),
    set(i, el) {
      setValue([...value.slice(0, i), el, ...value.slice(i + 1)]);
    },
    delete(i) {
      setValue([...value.slice(0, i), ...value.slice(i + 1)]);
    },
  };

  const p = new Proxy(value, {
    get: (obj, key) => {
      if (key in additional) {
        return additional[key];
      } else {
        return value[key];
      }
    },
  });
  return p;
}
