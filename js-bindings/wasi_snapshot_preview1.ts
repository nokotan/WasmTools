import { wasiInstance } from "./WASIModule";

console.log(wasiInstance.wasiImport)

export const { 
    fd_close, 
    fd_write, 
} = wasiInstance.wasiImport;

export const { 
    fd_fdstat_get, 
    fd_seek,
} = wasiInstance.wasiImport;
