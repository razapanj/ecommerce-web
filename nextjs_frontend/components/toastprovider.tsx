"use client"
import { ToastContainer } from 'react-toastify';
import { ReactElement } from 'react';
import 'react-toastify/dist/ReactToastify.css';

const ToastProvider = ({ children }: any) => {
    return (
        <>
            <ToastContainer />
            {children}
        </>
    );
};

export default ToastProvider;