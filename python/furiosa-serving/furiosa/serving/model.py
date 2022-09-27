from abc import ABC, abstractmethod
from typing import Any, Awaitable, Callable, Dict, List, Optional, Tuple, Union, overload

from fastapi import FastAPI
from fastapi.routing import Mount
import numpy as np

from furiosa.runtime.tensor import TensorDesc
from furiosa.server import ModelConfig, NuxModel, Model, NuxModelConfig


class ServeModel(ABC):
    def __init__(
        self,
        app: FastAPI,
        name: str,
        *,
        preprocess: Optional[Callable[[Any, Any], Awaitable[Any]]] = None,
        predict: Optional[Callable[[List[np.ndarray]], Awaitable[List[np.ndarray]]]] = None,
        postprocess: Optional[Callable[[Any, Any], Awaitable[Any]]] = None,
    ):
        self._app = app
        self._name = name
        self._routes: Dict[Callable, Callable] = {}

        async def identity(*args, **kwargs):
            return (*args, kwargs) if kwargs else args

        self._preprocess = preprocess or identity
        self._predict = predict
        self._postprocess = postprocess or identity

    async def preprocess(self, *args: Any, **kwargs: Any) -> Any:
        return await self._preprocess(args, kwargs)

    @abstractmethod
    async def predict(self, payload: List[np.ndarray]) -> List[np.ndarray]:
        ...

    async def postprocess(self, *args: Any, **kwargs: Any) -> Any:
        return await self._postprocess(args, kwargs)

    @property
    @abstractmethod
    def inner(self) -> Model:
        ...

    @property
    @abstractmethod
    def config(self) -> ModelConfig:
        ...

    @property
    @abstractmethod
    def inputs(self) -> List[TensorDesc]:
        ...

    @property
    @abstractmethod
    def outputs(self) -> List[TensorDesc]:
        ...

    def expose(self):
        """
        Expose FastAPI route API endpoint
        """
        for func, decorator in self._routes.items():
            # Decorate the path operation function to expose endpoint
            decorator(func)

    def hide(self):
        """
        Hide FastAPI route API endpoint
        """
        # Gather routes not in sub applications
        routes = [route for route in self._app.routes if not isinstance(route, Mount)]

        # Target routes to be removed
        targets = [route for route in routes if route.endpoint in self._routes]  # type: ignore

        # Unregister path operation functions to hide endpoint
        for route in targets:
            self._app.routes.remove(route)

    def _method(self, kind: str, *args, **kwargs) -> Callable:
        def decorator(func):
            """
            Register FastAPI path operation function to be used later.

            The function will be registerd into FastAPI app when model is loaded.
            """
            self._routes[func] = getattr(self._app, kind)(*args, **kwargs)
            return func

        return decorator

    def get(self, *args, **kwargs) -> Callable:
        return self._method("get", *args, **kwargs)

    def put(self, *args, **kwargs) -> Callable:
        return self._method("put", *args, **kwargs)

    def post(self, *args, **kwargs) -> Callable:
        return self._method("post", *args, **kwargs)

    def delete(self, *args, **kwargs) -> Callable:
        return self._method("delete", *args, **kwargs)

    def head(self, *args, **kwargs) -> Callable:
        return self._method("head", *args, **kwargs)

    def patch(self, *args, **kwargs) -> Callable:
        return self._method("patch", *args, **kwargs)

    def trace(self, *args, **kwargs) -> Callable:
        return self._method("trace", *args, **kwargs)


class NPUServeModel(ServeModel):
    def __init__(
        self,
        app: FastAPI,
        name: str,
        *,
        model: Union[str, bytes],
        version: Optional[str] = None,
        description: Optional[str] = None,
        npu_device: Optional[str] = None,
        compiler_config: Optional[Dict] = None,
        preprocess: Optional[Callable[[Any, Any], Awaitable[Any]]] = None,
        postprocess: Optional[Callable[[Any, Any], Awaitable[Any]]] = None,
    ):
        super().__init__(app, name, preprocess=preprocess, postprocess=postprocess)

        self._config = NuxModelConfig(
            name=name,
            model=model,
            version=version,
            description=description,
            npu_device=npu_device,
            compiler_config=compiler_config,
        )

        self._model = NuxModel(self._config)

    async def predict(self, payload: List[np.ndarray]) -> List[np.ndarray]:
        return await self._model.predict(payload)

    @property
    def inner(self) -> NuxModel:
        return self._model

    @property
    def config(self) -> NuxModelConfig:
        return self._config

    @property
    def inputs(self) -> List[TensorDesc]:
        # TODO(yan): Replace TensorDesc with abstract class like numpy.ndarray
        return self._model.session.inputs()

    @property
    def outputs(self) -> List[TensorDesc]:
        # TODO(yan): Replace TensorDesc with abstract class like numpy.ndarray
        return self._model.session.outputs()


class CPUServeModel(ServeModel):
    def __init__(
        self,
        app: FastAPI,
        name: str,
        *,
        predict: Callable[[List[np.ndarray]], Awaitable[List[np.ndarray]]],
        version: Optional[str] = None,
        description: Optional[str] = None,
        preprocess: Optional[Callable[[Any, Any], Awaitable[Any]]] = None,
        postprocess: Optional[Callable[[Any, Any], Awaitable[Any]]] = None,
    ):
        super().__init__(app, name, predict=predict, preprocess=preprocess, postprocess=postprocess)

        self._config = ModelConfig(
            name=name, version=version, description=description, platform="CPU"
        )

        self._model = CPUModel(self._config, predict=predict)

    async def predict(self, payload: List[np.ndarray]) -> List[np.ndarray]:
        return await self._model.predict(payload)

    @property
    def inner(self) -> Model:
        return self._model

    @property
    def config(self) -> ModelConfig:
        return self._config

    @property
    def inputs(self) -> List[TensorDesc]:
        raise NotImplementedError("CPUServerModel inputs() not yet supported")

    @property
    def outputs(self) -> List[TensorDesc]:
        raise NotImplementedError("CPUServerModel outputs() not yet supported")


class CPUModel(Model):
    def __init__(
        self,
        config: ModelConfig,
        *,
        predict: Callable[[List[np.ndarray]], Awaitable[List[np.ndarray]]],
    ):
        super().__init__(config)

        self._predict = predict

    async def predict(self, payload: List[np.ndarray]) -> List[np.ndarray]:
        return await self._predict(payload)
