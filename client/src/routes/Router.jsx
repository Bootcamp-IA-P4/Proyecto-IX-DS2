import React from "react";
import { createBrowserRouter } from "react-router-dom";
import Layout from "../layout/Layout";
import Home from "../pages/Home";
import Prediction from "../pages/Prediction";
import History from "../pages/History";

export const router = createBrowserRouter([
    {
        path: "/",
        element: <Layout />,
        children: [
            {
                index: true,
                element: <Home />
            },
            {
                path: "predict",
                element: <Prediction />
            },
            {
                path: "history",
                element: <History />
            }
        ]
    }
]);