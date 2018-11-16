# Adapted from jsonref (https://github.com/gazpachoking/jsonref)
# Licensed under MIT. Copyright (c) 2013 Chase Sterling

import typing
import re

from urllib import parse as urlparse
from urllib.parse import unquote

from collections import Sequence

T = typing.TypeVar('T')


def replace(document: T, root: typing.Dict=None) -> T:
    """
    Replace the JSON references in the specified document with actual objects.

    :param document: The document to replace the references in.
    :param root: The root of the document pointers are resolved relative to (default `document`).
    :return: The document with the JSON references replaced with actual objects.
    """
    if root is None:
        root = document

    if isinstance(document, dict):
        obj = {key: replace(value, root) for (key, value) in document.items()}

        base_refs = obj.get('$base')
        merge_keys = set(obj.get('$merge', []))

        if isinstance(base_refs, str):
            base_refs = [base_refs]

        # Ignore if $base is of different type
        if isinstance(base_refs, list):
            class Wrapper(dict):
                def __init__(self, refs):
                    super().__init__({})
                    self.__refs = refs

            wrapper = Wrapper(base_refs)
            for ref in base_refs:
                wrapper = merge(wrapper, resolve(root, ref), merge_keys)

            obj = merge(wrapper, obj, merge_keys)

            if '$base' in obj:
                del obj['$base']
            if '$merge' in obj:
                del obj['$merge']

        return obj
    elif isinstance(document, list):
        return [replace(value, root) for value in document]
    else:
        return document


def resolve(document, ref):
    """
    Resolve the specified URI reference in the given document (or use an external document).

    :param document: The document in which the URI reference was found.
    :param ref: The URI reference to resolve.
    :return: The resolved URI reference or `None`.
    """
    uri, fragment = urlparse.urldefrag(ref)

    if uri:
        raise NotImplemented("External URIs are not supported at the moment")
    return resolve_pointer(document, fragment)


def resolve_pointer(document, pointer: str):
    """
    Resolve a JSON pointer ``pointer`` within the referenced ``document``.

    :param document: the referent document
    :param str pointer: a json pointer URI fragment to resolve within it
    """
    root = document
    # Do only split at single forward slashes which are not prefixed by a caret
    parts = re.split(r"(?<!\^)/", unquote(pointer.lstrip("/"))) if pointer else []

    for part in parts:
        # Restore escaped slashes and carets
        replacements = {r"^/": r"/", r"^^": r"^"}
        part = re.sub(
            "|".join(re.escape(key) for key in replacements.keys()),
            lambda k: replacements[k.group(0)],
            part,
        )
        if isinstance(document, Sequence):
            # Try to turn an array index to an int
            try:
                part = int(part)
            except ValueError:
                pass

        try:
            document = document[part]
        except KeyError as e:
            raise KeyError(f"Pointer does not resolve to value: {pointer}") from e

    if document is root:
        # Prevents infinite recursion on same document
        return document
    else:
        return replace(document, root)


def merge(u: typing.Dict, v: typing.Dict, keys: typing.Set[str]) -> typing.Dict:
    """
    Merge the specified keys of the dictionaries one-level deep into the first dictionary. If the values at the key
    cannot be merged, prefer the second value.

    :param u: The first dictionary to merge in.
    :param v: The second dictionary to merge.
    :param keys: The keys to merge.
    """
    for (key, v_value) in v.items():
        if key in keys:
            u_value = u.get(key, None)

            if isinstance(u_value, list) and isinstance(v_value, list):
                u[key] = list(u_value + v_value)
                continue
            elif isinstance(u_value, dict) and isinstance(v_value, dict):
                u_value = u_value.copy()
                u_value.update(v_value)
                u[key] = u_value
                continue
        u[key] = v_value
    return u
